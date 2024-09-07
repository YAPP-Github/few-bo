//
//  MainView.swift
//  Few-iOS
//
//  Created by 송영모 on 9/7/24.
//

import Foundation
import SwiftUI

public struct MainView: View {
    @ObservedObject private var model: Model
    
    public init(model: Model) {
        self.model = model
    }
    
    public var body: some View {
        WebView(currentURL: self.model.currentURL)
            .frame(maxWidth: .infinity, maxHeight: .infinity)
            .ignoresSafeArea(.container, edges: .bottom)
            .onOpenURL { url in
                self.model.currentURL = url
            }
    }
}
