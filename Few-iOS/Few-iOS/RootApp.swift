//
//  RootApp.swift
//  Few-iOS
//
//  Created by 송영모 on 8/10/24.
//

import Foundation
import SwiftUI
import AppTrackingTransparency

@main
struct Few_iOSApp: App {
    @UIApplicationDelegateAdaptor(AppDelegate.self) var delegate
    @State var url = baseURL
    
    var body: some Scene {
        WindowGroup {
            ContentView(url: url)
                .frame(maxWidth: .infinity, maxHeight: .infinity)
                .ignoresSafeArea(.container, edges: .bottom)
                .onOpenURL { url in
                    self.url = url
                }
                .onReceive(NotificationCenter.default.publisher(for: UIApplication.didBecomeActiveNotification)) { _ in
                    ATTrackingManager.requestTrackingAuthorization(completionHandler: { _ in
                    })
                }
        }
        
    }
}

struct ContentView: View {
    var url: URL?
    
    var body: some View {
        if let url {
            WebView(url: url)
        }
    }
}
