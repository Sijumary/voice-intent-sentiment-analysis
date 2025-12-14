from app.services.analyze import analyze_text_and_audio




def test_analyze_cancel():
    fake_transcript = {'text': 'I want to cancel my subscription. I am not happy with the service.'}
    out = analyze_text_and_audio(fake_transcript, '/tmp/dummy.wav')


    assert out['intent'] == 'cancel_subscription'
    assert out['sentiment'] == 'negative'
    assert 'cancel' in out['summary'].lower()