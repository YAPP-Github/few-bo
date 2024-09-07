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
    
    var body: some Scene {
        WindowGroup {
            MainView(model: .init())
                .onReceive(
                    NotificationCenter
                        .default
                        .publisher(for: UIApplication.didBecomeActiveNotification)
                ) { _ in
                    ATTrackingManager
                        .requestTrackingAuthorization(
                            completionHandler: { _ in }
                        )
                }
        }
    }
}
