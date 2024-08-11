//
//  Few_iOSApp.swift
//  Few-iOS
//
//  Created by 송영모 on 8/1/24.
//

import SwiftUI
import AppTrackingTransparency

class AppDelegate: NSObject, UIApplicationDelegate {
    func application(_ application: UIApplication,
                     didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?) -> Bool {
        if ATTrackingManager.trackingAuthorizationStatus == .notDetermined {
        
        } else {
            ATTrackingManager.requestTrackingAuthorization { status in }
        }

      return true
    }
}
