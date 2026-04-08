from flask import Flask, render_template, request, redirect, url_for, session, flash
from services.vision_one_client import VisionOneClient, VisionOneClientError

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
    error_message = None
    query_form = {
        "query_type": "端點查詢",
        "time_range": "24h",
        "keyword": "",
        "endpoint_name": "",
        "note": "",
    }

    if request.method == "POST":
        query_form = {
            "query_type": request.form.get("query_type", "端點查詢"),
            "time_range": request.form.get("time_range", "24h"),
            "keyword": request.form.get("keyword", "").strip(),
            "endpoint_name": request.form.get("endpoint_name", "").strip(),
            "note": request.form.get("note", "").strip(),
        }

        try:
            client = VisionOneClient(
                token=settings.get("vision_one_token", ""),
                region=settings.get("vision_one_region", ""),
            )

            if query_form["query_type"] == "端點查詢":
                filter_parts = []
                if query_form["keyword"]:
                    filter_parts.append(query_form["keyword"])
                if query_form["endpoint_name"]:
                    filter_parts.append(f"endpointName eq '{query_form['endpoint_name']}'")
                filter_string = ' and '.join(filter_parts)
                result = client.query_endpoints(filter_string=filter_string)

            elif query_form["query_type"] == "Insight 查詢":
                result = client.query_insights(
                    time_range=query_form["time_range"],
                    filter_string=query_form["keyword"],
                )

            elif query_form["query_type"] == "Workbench 查詢":
                result = client.query_workbench_alerts(
                    time_range=query_form["time_range"],
                    filter_string=query_form["keyword"],
                )

            else:
                error_message = "目前第三版先支援：端點查詢、Insight 查詢、Workbench 查詢。"

        except VisionOneClientError as e:
            error_message = str(e)
        except Exception as e:
            error_message = f"查詢時發生未預期錯誤：{e}"

    return render_template(
        "query.html",
        settings=settings,
        query_form=query_form,
        result=result,
        error_message=error_message,
    )


@app.route("/result")
def result_page():
    return render_template("result.html", settings=get_settings())


@app.route("/about")
def about_page():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
