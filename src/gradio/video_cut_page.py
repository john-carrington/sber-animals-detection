import gradio as gr
import requests as r


def predict(video, step_seconds):
    headers = {
        'accept': 'application/json', }

    files = {'file': open(video, 'rb'), 'type': 'video/mp4'}
    response = r.post(f'http://127.0.0.1:8000/process_video?step_seconds={step_seconds}',
                      headers=headers, files=files).json()['file_path']
    return response


video_cut = gr.Interface(
    predict,
    inputs=[gr.File(
        file_count='single',
        file_types=['video', '.zip']), gr.Text()],
    outputs=gr.File(),


)
