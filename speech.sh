curl -X POST \
--data-binary @audio/output.flac \
--header 'Content-Type: audio/x-flac; rate=16000;' \
'https://www.google.com/speech-api/v2/recognize?output=json&lang=en-us&key=AIzaSyD6Cba8xQZUMnw_FUEaeJOTOz-kBMIf6l4'
