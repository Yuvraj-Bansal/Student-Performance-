from flask import Flask, request, render_template

from src.pipeline.predict_pipeline import CustomData, PredictPipeline


application = Flask(__name__)

app = application


def get_performance_level(score):
    if score >= 90:
        return "Excellent"
    elif score >= 75:
        return "Good"
    elif score >= 60:
        return "Average"
    else:
        return "Needs Improvement"


def get_recommendation(score):
    if score >= 90:
        return "Excellent performance. Keep maintaining your current study routine."
    elif score >= 75:
        return "Good performance. Regular mathematics practice can help you improve further."
    elif score >= 60:
        return "Average performance. Focus on regular practice and strengthening your fundamentals."
    else:
        return "Focus on mathematics fundamentals and practice consistently to improve your performance."


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predictdata', methods=['GET', 'POST'])
def predict_datapoint():

    if request.method == 'GET':
        return render_template('home.html')

    else:
        data = CustomData(
            gender=request.form.get('gender'),
            race_ethnicity=request.form.get('ethnicity'),
            parental_level_of_education=request.form.get(
                'parental_level_of_education'
            ),
            lunch=request.form.get('lunch'),
            test_preparation_course=request.form.get(
                'test_preparation_course'
            ),

            # Fixed: these were swapped before
            reading_score=float(request.form.get('reading_score')),
            writing_score=float(request.form.get('writing_score'))
        )

        pred_df = data.get_data_as_data_frame()

        predict_pipeline = PredictPipeline()

        results = predict_pipeline.predict(pred_df)

        predicted_score = round(float(results[0]), 2)

        performance_level = get_performance_level(predicted_score)

        recommendation = get_recommendation(predicted_score)

        return render_template(
            'home.html',
            results=predicted_score,
            performance_level=performance_level,
            recommendation=recommendation
        )


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)