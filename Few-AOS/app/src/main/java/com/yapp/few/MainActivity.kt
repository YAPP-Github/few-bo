package com.yapp.few

import android.content.Intent
import android.net.Uri
import android.os.Bundle
import android.webkit.WebView
import android.webkit.WebViewClient
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.viewinterop.AndroidView
import com.yapp.few.ui.theme.FewTheme

class MainActivity : ComponentActivity() {
    private var webViewUrl: String = "https://www.fewletter.com"

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        // 인텐트에서 URL을 추출
        intent?.data?.let { uri: Uri ->
            webViewUrl = uri.toString()
        }

        setContent {
            FewTheme {
                WebViewContainer(url = webViewUrl)
            }
        }
    }

    override fun onResume() {
        super.onResume()

        // onResume에서 인텐트를 다시 확인하여 URL을 처리
        intent?.data?.let { uri: Uri ->
            webViewUrl = uri.toString()
            setContent {
                FewTheme {
                    WebViewContainer(url = webViewUrl)
                }
            }
        }
    }

    @Composable
    fun WebViewContainer(url: String) {
        AndroidView(
            modifier = Modifier.fillMaxSize(),
            factory = { context ->
                WebView(context).apply {
                    settings.javaScriptEnabled = true
                    webViewClient = CustomWebViewClient()
                    loadUrl(url)
                }
            }
        )
    }

    private class CustomWebViewClient : WebViewClient() {
        override fun shouldOverrideUrlLoading(view: WebView?, url: String?): Boolean {
            if (url != null && !url.contains("fewletter.com")) {
                view?.context?.startActivity(Intent(Intent.ACTION_VIEW, Uri.parse(url)))
                return true
            }
            return false
        }
    }
}