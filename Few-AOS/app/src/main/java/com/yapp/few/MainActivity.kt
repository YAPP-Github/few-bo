package com.yapp.few

import android.annotation.SuppressLint
import android.content.Intent
import android.net.Uri
import android.os.Bundle
import android.webkit.WebView
import android.webkit.WebViewClient
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.Scaffold
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.viewinterop.AndroidView
import com.yapp.few.ui.theme.FewTheme

class MainActivity : ComponentActivity() {
    @SuppressLint("UnusedMaterial3ScaffoldPaddingParameter")
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        setContent {
            FewTheme {
                Scaffold(modifier = Modifier.fillMaxSize()) {
                    WebViewContainer(url = "https://www.fewletter.com")
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