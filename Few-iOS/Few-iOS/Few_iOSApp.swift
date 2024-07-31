//
//  Few_iOSApp.swift
//  Few-iOS
//
//  Created by 송영모 on 8/1/24.
//

import SwiftUI

@main
struct Few_iOSApp: App {
    var body: some Scene {
        WindowGroup {
            if let url = URL(string: "https://www.fewletter.com") {
                WebView(url: url)
                    .frame(maxWidth: .infinity, maxHeight: .infinity)
                    .ignoresSafeArea(.container, edges: .bottom)
            }
        }
    }
}
