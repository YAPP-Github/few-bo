import SwiftUI
import WebKit
import AppTrackingTransparency

// Constants
let baseURLString = "https://www.fewletter.com/"
public let baseURL = URL(string: baseURLString)!

@main
struct Few_iOSApp: App {
    @State private var webView: WebView?
    @State private var urls: [URL] = []
    
    var body: some Scene {
        WindowGroup {
            NavigationStack(path: $urls) {
                if let webView = webView {
                    webView
                        .ignoresSafeArea()
                        .navigationDestination(for: URL.self) { url in
                            print("navigate: \(url)")
                            return WrappedView(content: {
                                webView
                            })
                        }
                }
            }
            .onAppear {
                self.webView = .init(url: baseURL, onURLChanged: self.handleURL(url:))
            }
        }
    }
    
    private func handleURL(url: URL) {
        print("handleURL: \(url)")
        guard self.urls.last != url, url != baseURL else { return }
        
        let urlCount = self.urls.count
        
        guard urlCount - 2 > 0 else {
            urls.append(url)
            return
        }
        
        if urls[urlCount - 2] == url {
            urls.removeLast()
        }
    }
}

struct WrappedView<Content: View>: View {
    var content: () -> Content
    
    var body: some View {
        content()
    }
}

struct WebView: UIViewRepresentable {
    var url: URL
    
    public var onURLChanged: (URL) -> Void
    
    func makeUIView(context: Context) -> WKWebView {
        let webView = WKWebView()
        webView.navigationDelegate = context.coordinator
        webView.allowsBackForwardNavigationGestures = true
        webView.addObserver(context.coordinator, forKeyPath: #keyPath(WKWebView.url), options: .new, context: nil)
        webView.load(URLRequest(url: url))
        return webView
    }
    
    func updateUIView(_ webView: WKWebView, context: Context) {
        if webView.url != url {
            webView.load(URLRequest(url: url))
        }
    }
    
    func makeCoordinator() -> Coordinator {
        Coordinator(self)
    }
    
    class Coordinator: NSObject, WKNavigationDelegate {
        var parent: WebView
        
        init(_ parent: WebView) {
            self.parent = parent
        }
        
        override func observeValue(forKeyPath keyPath: String?, of object: Any?, change: [NSKeyValueChangeKey : Any]?, context: UnsafeMutableRawPointer?) {
            if keyPath == #keyPath(WKWebView.url), let newURL = change?[.newKey] as? URL {
                self.parent.onURLChanged(newURL)
            }
        }
        
        func webView(_ webView: WKWebView, decidePolicyFor navigationAction: WKNavigationAction, decisionHandler: @escaping (WKNavigationActionPolicy) -> Void) {
            if let url = navigationAction.request.url, url.host != baseURL.host {
                UIApplication.shared.open(url)
                decisionHandler(.cancel)
            } else {
                decisionHandler(.allow)
            }
        }
        
        func webView(_ webView: WKWebView, didFinish navigation: WKNavigation!) {
            if let currentURL = webView.url {
                print("Navigation finished with URL: \(currentURL.absoluteString)")
            }
        }
    }
}
