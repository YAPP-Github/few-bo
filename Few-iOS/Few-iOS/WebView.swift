//
//  WebView.swift
//  Few-iOS
//
//  Created by 송영모 on 8/1/24.
//

import Foundation
import SwiftUI
import WebKit

let baseURLString = "https://www.fewletter.com"
public let baseURL = URL(string: baseURLString)!

struct WebView: UIViewRepresentable {
    let url: URL
    let webView: WKWebView = .init()

    init(url: URL) {
        self.url = url
    }

    func makeUIView(context: Context) -> WKWebView {
        webView.navigationDelegate = context.coordinator
        webView.allowsBackForwardNavigationGestures = true
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

        func webView(_ webView: WKWebView, decidePolicyFor navigationAction: WKNavigationAction, decisionHandler: @escaping (WKNavigationActionPolicy) -> Void) {
            if let url = navigationAction.request.url, let host = url.host {
                if host != URL(string: baseURLString)?.host {
                    UIApplication.shared.open(url)
                    decisionHandler(.cancel)
                    return
                }
            }
            decisionHandler(.allow)
        }
    }
}
