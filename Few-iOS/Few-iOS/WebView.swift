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
    let webView: WKWebView = .init()
    let url: URL
    
    init(url: URL) {
        self.url = url
    }
    
    func makeUIView(context: Context) -> WKWebView {
        let request = URLRequest(url: url)
        webView.isInspectable = true
        webView.isOpaque = false
        webView.backgroundColor = .clear
        webView.load(request)
        return webView
    }
    
    func update(url: URL) {
        let request = URLRequest(url: url)
        webView.load(request)
    }
    
    func updateUIView(_ webView: WKWebView, context: Context) {
        
    }
}
