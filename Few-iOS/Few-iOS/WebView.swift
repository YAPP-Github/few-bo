//
//  WebView.swift
//  Few-iOS
//
//  Created by 송영모 on 8/1/24.
//

import Foundation
import SwiftUI
import WebKit

struct WebView: UIViewRepresentable {
    let baseURL: URL
    let currentURL: URL
    let webView: WKWebView = .init()
    
    private let cookieClient: CookieClient

    init(baseURL: URL = .base, currentURL: URL) {
        self.baseURL = baseURL
        self.currentURL = currentURL
        
        self.cookieClient = CookieClientLive()
    }

    func makeUIView(context: Context) -> WKWebView {
        webView.navigationDelegate = context.coordinator
        webView.allowsBackForwardNavigationGestures = true
        webView.load(URLRequest(url: currentURL))
        let refreshControl = UIRefreshControl()
        refreshControl.addTarget(self, action: #selector(WKWebView.reloadWebView(_:)), for: .valueChanged)
        webView.scrollView.addSubview(refreshControl)
        return webView
    }
    
    private func setAuthCookies() {
        let refreshToken = UserDefaults.standard.value(forKey: "refreshToken") as? String
        let accessToken = UserDefaults.standard.value(forKey: "accessToken") as? String
        
        if let refreshToken {
            let cookie: [HTTPCookiePropertyKey: Any] = [
                .domain: baseURL.absoluteString,
                .path: "/",
                .name: "refreshToken",
                .value: refreshToken,
            ]
            if let cookie = HTTPCookie(properties: cookie) {
                webView.configuration.websiteDataStore.httpCookieStore.setCookie(cookie)
            }
        }
        if let accessToken {
            let cookie: [HTTPCookiePropertyKey: Any] = [
                .domain: baseURL.absoluteString,
                .path: "/",
                .name: "accessToken",
                .value: accessToken,
            ]
            if let cookie = HTTPCookie(properties: cookie) {
                webView.configuration.websiteDataStore.httpCookieStore.setCookie(cookie)
            }
        }
    }
    
    @MainActor
    private func interceptAuthCookies() {
        Task {
            let cookies = await cookieClient.getCookies(store: webView.configuration.websiteDataStore.httpCookieStore)
            for cookie in cookies {
                switch cookie.name {
                case "refreshToken":
                    UserDefaults.standard.setValue("refreshToken", forKey: cookie.value)
                case "accessToken":
                    UserDefaults.standard.setValue("accessToken", forKey: cookie.value)
                default:
                    continue
                }
            }
            print(cookies)
        }
    }

    func updateUIView(_ webView: WKWebView, context: Context) {
        if webView.url != currentURL {
            webView.load(URLRequest(url: currentURL))
        }
    }

    func makeCoordinator() -> Coordinator {
        Coordinator(self, baseURL: baseURL)
    }

    class Coordinator: NSObject, WKNavigationDelegate {
        var parent: WebView
        let baseURL: URL
        
        init(_ parent: WebView, baseURL: URL) {
            self.parent = parent
            self.baseURL = baseURL
        }

        func webView(
            _ webView: WKWebView,
            decidePolicyFor navigationAction: WKNavigationAction,
            decisionHandler: @escaping (WKNavigationActionPolicy) -> Void
        ) {
            if let url = navigationAction.request.url, let host = url.host {
                if host != baseURL.host {
                    UIApplication.shared.open(url)
                    decisionHandler(.cancel)
                    return
                }
            }
            decisionHandler(.allow)
        }
    }
}

extension WKWebView {
    @objc func reloadWebView(_ sender: UIRefreshControl) {
        self.reload()
        sender.endRefreshing()
    }
}
