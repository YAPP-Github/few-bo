//
//  Model.swift
//  Few-iOS
//
//  Created by 송영모 on 9/7/24.
//

import Foundation

extension URL {
    static let base: Self = URL(string: "https://www.fewletter.com")!
}

public class Model: ObservableObject {
    @Published public var currentURL: URL
    
    init(currentURL: URL = .base) {
        self.currentURL = currentURL
    }
}
