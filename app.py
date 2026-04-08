from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = "change-me-before-production"


def get_settings():
    return {
        "vision_one_token": session.get("vision_one_token", ""),
        "vision_one_region": session.get("vision_one_region", ""),
        "ai_endpoint_key": session.get("ai_endpoint_key", ""),
        "customer_name": session.get("customer_name", ""),
    }


@app.route("/")
def home():
    settings = get_settings()
    configured = bool(settings["vision_one_token"])
    return render_template("index.html", settings=settings, configured=configured)


@app.route("/settings", methods=["GET", "POST"])
def settings_page():
    if request.method == "POST":
        session["vision_one_token"] = request.form.get("vision_one_token", "").strip()
        session["vision_one_region"] = request.form.get("vision_one_region", "").strip()
        session["ai_endpoint_key"] = request.form.get("ai_endpoint_key", "").strip()
        session["customer_name"] = request.form.get("customer_name", "").strip()
        flash("設定已暫存於目前瀏覽工作階段，未寫入磁碟。", "success")
        return redirect(url_for("settings_page"))

    return render_template("settings.html", settings=get_settings())


@app.route("/settings/clear", methods=["POST"])
def clear_settings():
    for key in ["vision_one_token", "vision_one_region", "ai_endpoint_key", "customer_name"]:
        session.pop(key, None)
    flash("已清除目前工作階段中的敏感設定。", "success")
    return redirect(url_for("settings_page"))


@app.route("/query", methods=["GET", "POST"])
def query_page():
    settings = get_settings()
    result = None
    query_form = {
        "query_type": "事件查詢",
        "time_range": "24h",
        "keyword": "",
        "endpoint_name": "",
        "note": "",
    }

    if request.method == "POST":
        query_form = {
            "query_type": request.form.get("query_type", "事件查詢"),
            "time_range": request.form.get("time_range", "24h"),
            "keyword": request.form.get("keyword", "").strip(),
            "endpoint_name": request.form.get("endpoint_name", "").strip(),
            "note": request.form.get("note", "").strip(),
        }

        result = {
            "status": "success",
            "message": "這是第一版介面示範。目前先保留查詢流程與欄位，下一步再串接實際 Vision One API。",
            "settings_summary": {
                "customer_name": settings.get("customer_name") or "未設定",
                "vision_one_region": settings.get("vision_one_region") or "未設定",
                "vision_one_token": "已輸入" if settings.get("vision_one_token") else "未輸入",
            },
            "query_form": query_form,
            "mock_results": [
                {
                    "標題": "查詢流程已建立",
                    "內容": "目前頁面已可接收查詢條件，下一版可直接串 Vision One API。",
                },
                {
                    "標題": "敏感資訊處理",
                    "內容": "Token 與 Key 僅暫存在 session，不會寫入專案檔案。",
                },
            ],
        }

    return render_template("query.html", settings=settings, query_form=query_form, result=result)


@app.route("/result")
def result_page():
    return render_template("result.html", settings=get_settings())


@app.route("/about")
def about_page():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)
