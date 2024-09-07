//
//  CookieClient.swift
//  Few-iOS
//
//  Created by 송영모 on 9/7/24.
//

import Foundation
import WebKit

public protocol CookieClient {
    func getCookies(store: WKHTTPCookieStore) async -> [HTTPCookie]
//    func setCookies(store: WKHTTPCookieStore, keys: [String])
}

public class CookieClientLive: CookieClient {
    public func getCookies(store: WKHTTPCookieStore) async -> [HTTPCookie] {
        return await withCheckedContinuation { continuation in
            store.getAllCookies { cookies in
                continuation.resume(returning: cookies)
            }
        }
    }
    
//    func setCookies(store: WKHTTPCookieStore) {
//        let cookie: [HTTPCookiePropertyKey: Any] = [
//            .domain: // host (String),
//            .path: // path (String),
//            .name: "JSESSIONID",
//            .value: // cookie name에 해당하는 value (String)
//        ]
//
//        if let cookie = HTTPCookie(properties: cookie) {
//            webView.configuration.websiteDataStore.httpCookieStore.setCookie(cookie)
//        }
//    }
     
     
//    func saveCookie() {
//        let cookieStore = webView.configuration.websiteDataStore.httpCookieStore
//
//        cookieStore.getAllCookies { cookies in
//            for cookie in cookies {
//                if cookie.name == "JSESSIONID" {
//                    // UserDefault를 통해 앱 내에 쿠키 값 저장
//                }
//                print("cookie name: \(cookie.name), cookie value: \(cookie.value)")
//            }
//        }
//    }

}
