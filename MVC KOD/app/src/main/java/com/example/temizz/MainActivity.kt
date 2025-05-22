package com.example.temizz  // kendi paket adını yazmayı unutma

import android.app.Activity
import android.content.Intent
import android.graphics.BitmapFactory
import android.net.Uri
import android.os.Bundle
import android.provider.MediaStore
import android.widget.Button
import android.widget.ImageView
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.bumptech.glide.Glide
import com.github.dhaval2404.imagepicker.ImagePicker  // ✅ bu doğru
import okhttp3.*
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.RequestBody.Companion.asRequestBody
import org.json.JSONObject
import java.io.File
import java.io.IOException


class MainActivity : AppCompatActivity() {

    private lateinit var imageView: ImageView
    private lateinit var resultText: TextView
    private val client = OkHttpClient()
    private val serverUrl = "http://192.168.147.153:5000"  // Emülatör için doğru IP
    private val PICK_IMAGE = 1001

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        imageView = findViewById(R.id.imageView)
        resultText = findViewById(R.id.resultText)

        val btnSelect = findViewById<Button>(R.id.btnOpenCameraGallery)
        val btnSimulate = findViewById<Button>(R.id.btnOpenSimulation)

        btnSelect.setOnClickListener {
            ImagePicker.with(this)
                //.crop()
                .galleryOnly()
                .start()
        }

        btnSimulate.setOnClickListener {
            resultText.text = "Simülasyon çalıştı! (Örnek sonuç)"
        }
    }

    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)

        if (resultCode == Activity.RESULT_OK && data != null) {
            val uri = data.data!!
            val file = File(uri.path!!)

            val inputStream = contentResolver.openInputStream(uri)
            val bitmap = BitmapFactory.decodeStream(inputStream)
            imageView.setImageBitmap(bitmap)

            uploadImageToServer(file)
        }
    }

    private fun uploadImageToServer(file: File) {
        val requestBody = MultipartBody.Builder()
            .setType(MultipartBody.FORM)
            .addFormDataPart("image", file.name, file.asRequestBody("image/*".toMediaType()))
            .build()

        val request = Request.Builder()
            .url("$serverUrl/check-defect")
            .post(requestBody)
            .build()

        client.newCall(request).enqueue(object : Callback {
            override fun onFailure(call: Call, e: IOException) {
                runOnUiThread {
                    Toast.makeText(this@MainActivity, "Hata: ${e.message}", Toast.LENGTH_SHORT).show()
                }
            }

            override fun onResponse(call: Call, response: Response) {
                val responseBody = response.body?.string()
                if (response.isSuccessful && responseBody != null) {
                    val json = JSONObject(responseBody)
                    val ratio = json.getDouble("defect_ratio")
                    val imageUrl = "$serverUrl/result-image"

                    runOnUiThread {
                        resultText.text = "Hata Oranı: %.2f%%".format(ratio)
                        loadImageFromUrl(imageUrl)
                    }
                } else {
                    runOnUiThread {
                        Toast.makeText(this@MainActivity, "Sunucu hatası!", Toast.LENGTH_SHORT).show()
                    }
                }
            }
        })
    }

    private fun loadImageFromUrl(url: String) {
        Glide.with(this)
            .load(url)
            .into(imageView)
    }
}
