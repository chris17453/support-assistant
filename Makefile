


phony: .

clean:
	@-rm assets/database/assistant.db
	@-rm -rf assets/audio/*
	@-rm -rf assets/video/*
	@-rm -rf assets/image/*
	@-rm -rf sessions/*

help:
	@-python -m assistant.utils -h

init:
	@-python -m assistant.utils db --init

populate: clean init owner link voice account avatar image 
#video audio

list:  list_owners list_links list_voices list_accounts list_avatars list_images list_utterances list_video list_audio

owner:
	@-python -m assistant.utils insert_owner --active --name "Chris" --description 'Root instance'

list_owners:
	@-python -m assistant.utils list_owners

link:
	@-python -m assistant.utils insert_link --name User1 --owner-id 1 --description 'First user' --active

list_links:
	@-python -m assistant.utils list_links

voice:
	@-python -m assistant.utils insert_voice --name 'ChrisReal'   --gender male   --description 'Default' --voice 'en-US-Wavenet-I'  --account-id 1 --active --link-id 1
	@-python -m assistant.utils insert_voice --name 'AltarAI'     --gender male   --description 'Default' --voice 'en-AU-News-G'     --account-id 1 --active --link-id 1
	@-python -m assistant.utils insert_voice --name 'ChristinaAI' --gender female --description 'Default' --voice 'en-IN-Standard-C' --account-id 1 --active --link-id 1
	@-python -m assistant.utils insert_voice --name 'ChrisAI'     --gender male   --description 'Default' --voice 'en-GB-News-M'     --account-id 1 --active --link-id 1

list_voices:
	@-python -m assistant.utils list_voices


account:
	@-python -m assistant.utils insert_account --name GoogleVoice --description 'Google voice provider' --json '/home/nd/repos/Projects/support-assistant/credentials/robotshop-378518-af03d284fd3b.json'  --platform 'Google' --active --link-id 1
	@-python -m assistant.utils insert_account --name OpenAI --description 'OpenAI ChatGPT  provider' --api-key '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' --platform 'OpenAI' --active --link-id 1

list_accounts:
	@-python -m assistant.utils list_accounts


avatar:
	@-python -m assistant.utils insert_avatar --name ChrisIRL    --description 'Chris Real'        --active --link-id 1 --image-id 1 --voice-id 1 --pitch 1 --speed 1 --style Default
	@-python -m assistant.utils insert_avatar --name AltarAI     --description 'Altar AI Gen1'     --active --link-id 1 --image-id 2 --voice-id 1 --pitch 1 --speed 1 --style Default
	@-python -m assistant.utils insert_avatar --name ChristinaAI --description 'Christina AI Gen1' --active --link-id 1 --image-id 3 --voice-id 1 --pitch 1 --speed 1 --style Default
	@-python -m assistant.utils insert_avatar --name ChrisAI     --description 'Chris AI Gen1'     --active --link-id 1 --image-id 4 --voice-id 1 --pitch 1 --speed 1 --style Default

list_avatars:
	@-python -m assistant.utils list_avatars


image:
	@-python -m assistant.utils insert_image --name 'Chris Real'        --description 'Chris Real'         --path '/home/nd/repos/Projects/support-assistant/assets/master/image/chrisirl.jpg'   --active --link-id 1 
	@-python -m assistant.utils insert_image --name 'Altar AI Gen1'     --description 'Altar AI Gen1'      --path '/home/nd/repos/Projects/support-assistant/assets/master/image/avatar2.png' --active --link-id 1 
	@-python -m assistant.utils insert_image --name 'Christina AI Gen1' --description 'Christina AI Gen1'  --path '/home/nd/repos/Projects/support-assistant/assets/master/image/avatar3.png' --active --link-id 1 
	@-python -m assistant.utils insert_image --name 'Chris AI Gen1    ' --description 'Chris AI Gen1'      --path '/home/nd/repos/Projects/support-assistant/assets/master/image/avatar4.png' --active --link-id 1 

list_images:
	@-python -m assistant.utils list_images

utterance:
	@-python -m assistant.utils insert_utterance --text "Hello, I'm Chris" --count 3 --variance 1 --avatar-id 1 --link-id  1 --active 

list_utterances:
	@-python -m assistant.utils list_utterances

video:
	@-python -m assistant.utils insert_video --path '/home/nd/repos/Projects/assistant/assets/videos/out-e.mp4'  --link-id  1 --active 

list_video:
	@-python -m assistant.utils list_videos

audio:
	@-python -m assistant.utils insert_audio --path '/home/nd/repos/Projects/assistant/assets/audio/48889499-f16f-43a1-9c13-77f0e89e6281.wav'  --link-id  1 --active 

list_audio:
	@-python -m assistant.utils list_audio


process-batch:
	@-python -m assistant.utils process-batch --avatar-id 4  --file assets/batch/dubs.txt

process-long:
	python -m assistant.utils process --avatar-id 1	--text "In the tranquil meadow, under the azure sky dotted with fluffy white clouds, a gentle breeze rustles the vibrant grass, carrying the sweet scent of wildflowers. Bees buzz busily from blossom to blossom, diligently collecting nectar to make golden honey. Birds chirp melodiously, their songs harmonizing with the rustling leaves of the tall, majestic trees that provide shade and shelter. Sunlight filters through the branches, casting dappled shadows on the emerald carpet below. Nature's symphony unfolds, captivating the senses and filling the heart with tranquility, reminding us of the beauty and wonder that surrounds us every day. Please note that the above sentence may not have exactly one hundred words, as it is difficult to construct a sentence with precisely that word count while maintaining readability. However, it provides an example of a descriptive sentence that is relatively long and captures the essence of a tranquil natural setting"

upload:
	@rsync -ahuv  /home/nd/repos/Projects/support-assistant 10.90.0.80:/web/
	@ssh root@10.90.0.80 'chown -R nginx:nginx /web/support-assistant/'


