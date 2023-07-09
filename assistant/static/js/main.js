 class chris_entity{
    constructor(player_id,history_id,action_id,avatar_selector){
        this.instance_id =
        this.avatar_selector = document.getElementById(avatar_selector);
        this.video_player = document.getElementById(player_id);
        this.output      = document.getElementById(history_id);
        this.action      = document.getElementById(action_id);
        this.recognition = new webkitSpeechRecognition();
        this.video_player_id=player_id;

        this.recognition.continuous = false;

        this.recognition.interimResults = false;
        
        this.start_speech= true;
        this.is_playing=false;
        this.instance_id=this.generate_UUID();
        this.human_name="Chris";
        this.other_name="User"
        this.other_id=1234
        this.message_history=[];
          
        this.get_token();
   
        

        // add event handlers for the speech recognition
        this.recognition.onstart = () => {
        }
        
        this.recognition.onresult = (e) => {
            console.log("Speech has returned a result");
            var transcript = e.results[e.results.length-1][0].transcript;
            this.chat_add_line(this.other_name,this.other_id,transcript)
            this.talk_to_bot(transcript)
        }
        
        this.recognition.addEventListener("speechend", () => {
            console.log("Speech has ended");
            this.start_speech=true; 
        });

        this.video_player.addEventListener('ended', (event) => {
            console.log("Video has ended.");
            this.is_playing=false;
      
            this.start_listening();
        });
      

        this.avatar_selector.addEventListener('change',this.load_avatar.bind(this));
        // Set an interval to call the checkFlag function every second (1000 milliseconds)
        //this.speech_interval_id = setInterval(this.check_listening.bind(this), 1000); 
        //this.webcam_shake_id = setInterval(this.shake_webcam.bind(this), 11000); 
        
        this.speech_timer = false;
        this.speech_index = 0;
    }

    start_listening(){
        console.log("Listening")
        try{
            this.recognition.start();
        }catch(err){
            console.log(err)
        }
    }

    stop_listening(){
        console.log("Not Listening")
        this.recognition.stop();
    }


    play(data){
        console.log(data);
        this.video_start(data.video)
        this.chat_add_line(this.human_name,this.instance_id,data.content)
    }
    play_audio(data){
        console.log(data);
        this.stop_listening();
        console.log(data.audio);
        var audio = new Audio("audio/"+data.audio);
        // Attach event listener for 'ended' event
        audio.addEventListener('ended', this.stop_audio.bind(this));            
        audio.play();
        this.chat_add_line(this.human_name,this.instance_id,data.content)
    }

    stop_audio(){
        console.log('Audio playback finished'); // You can replace this with your own function call
        this.start_listening();
    }

    talk_to_bot(transcript){
        console.log("Talking to Server")
        return $.ajax({
           url: 'api/talk',
           type: "POST",
           dataType: "json",
           contentType: "application/json",
           headers: {
                 'Authorization': 'Bearer ' + localStorage.getItem('access_token')
           },           
           data: JSON.stringify(transcript)
         }).done($.proxy(this.play,this))
         .fail(function(xhr, status, error) {
           console.error(error); // Handle any errors here
         });
    }


    video_start(video_id=null) {
        console.log("Start Video");
        this.stop_listening();
        if(video_id!=null) 
            this.video_player.src="video/"+video_id;
        this.video_player.load();
        this.is_playing=true;
    }

    video_stop() {
        console.log("Stop Video")
        this.video_player.pause();
        this.is_playing=false;
        this.start_listening();
    }


    video(video_id){
        console.log("Play Video")
        this.video_player.pause();
        this.video_player.src = video_id;
        this.video_player.load();
        this.is_playing=true;
        this.stop_listening();
    }


    check_listening() { 
         this.speech_index++;
        console.log(this.speech_index+' Checking if speech recognition is running...');
        if (this.is_playing==false && this.start_speech==true) {
          console.log('Restarting Speech!');
          // clear  the interval if flag is true
          //clearInterval(this.speech_interval_id)

          this.start_listening();
        }
      }

    generate_UUID() {
        const cryptoObj = window.crypto || window.msCrypto; // For browser compatibility
        const array = new Uint8Array(16);
        cryptoObj.getRandomValues(array);
      
        // Set the version and variant bits
        array[6] = (array[6] & 0x0f) | 0x40;
        array[8] = (array[8] & 0x3f) | 0x80;
      
        let uuid = '';
        for (let i = 0; i < 16; i++) {
          uuid += array[i].toString(16).padStart(2, '0');
        }
      
        return uuid;
    }

    chat_add_line(user,user_id,text){
        this.message_history.push({'role':'user','content':text})
        let user_class="";
        if(user_id==this.instance_id) user_class="chris_text";
        else user_class="other_text";
        this.output.innerHTML+=`<span class='${user_class}'>${user}:</span> ${text}</br>`;
        this.output.scrollTop = this.output.scrollHeight;

    }
    
  
      /*document.addEventListener('visibilitychange', function() {
          if (document.hidden) {
              console.log('Tab is now inactive');
              recognition.stop();
          } else {
              console.log('Tab is now active');
              recognition.start();
          }
      });*/
  

    get_token(){
      $.ajax({
        url: 'access_token',
        type: 'POST',
        contentType: 'application/json',
        success: function(response) {
          // Store the JWT token in local storage
          localStorage.setItem('access_token', response.access_token);
          console.log("Access token"+response.access_token)
  
        },
        error: function(xhr, status, error) {
          console.error(xhr.responseText); // Handle login error
        }
      });
    }

    shake_webcam() {
        var l = 20;  // change in pixels
        var t = 500; // change time in milliseconds
        var webcamDiv = $("#"+this.video_player_id);
    
        var originalPosition = webcamDiv.css('position');
        var originalTop = webcamDiv.css('top');
        var originalLeft = webcamDiv.css('left');
    
        webcamDiv.css('position', 'relative');
        
        for( var iterations=0 ; iterations<2 ; iterations++ ) {
            webcamDiv.animate({ left: "-=" + l }, t );
            webcamDiv.animate({ top: "+=" + l }, t );
            webcamDiv.animate({ left: "+=" + l }, t );
            webcamDiv.animate({ top: "-=" + l }, t );
        }
        
        webcamDiv.animate({ left: 0, top: 0 }, t, function() {
            // Restore original position
            webcamDiv.css('position', originalPosition);
            webcamDiv.css('top', originalTop);
            webcamDiv.css('left', originalLeft);
        });
    }

    set_persona(persona){
        console.log("Setting Persona now")
    }

    load_avatar(event){
        var avatar_uuid = this.avatar_selector.value;

        console.log("Avatar ID:"+avatar_uuid)
        return $.ajax({
           url: 'api/avatar',
           type: "POST",
           dataType: "json",
           contentType: "application/json",
           headers: {
                 'Authorization': 'Bearer ' + localStorage.getItem('access_token')
           },           
           data: JSON.stringify({avatar:avatar_uuid})
         }).done($.proxy(this.set_poster,this))
         .fail(function(xhr, status, error) {
           console.error(error); // Handle any errors here
         });
    }

    set_poster(data){
        console.log("Setting Poster")
        this.video_player.poster="image/"+data.poster;

    }



 
}


$(document).ready(function() {
/*    $("#text-input").keypress(function(event) {
    if (event.keyCode == 13) { // 13 is the ASCII code for enter
        event.preventDefault(); // Prevents the form from being submitted

        var text = $("#text-input").val();
        $("#text-input").val(''); // Clear the input field

        $.ajax({
        url: 'http://localhost:5000/change_video',
        type: 'post',
        contentType: 'application/json',
        data: JSON.stringify({'text': text}),
        success: function(data) {
            $("#video-player").attr('src', data.new_video_source);
        }
        });
    }
    });

*/
    // start listening an sending the results to the server
    chris=new chris_entity("chris_video","conversation_history","conversation_action", "avatar-persona")

    navigator.mediaDevices.getUserMedia({ video: true })
    .then(function (stream) {
        var videoElement = document.getElementById('user_video');
        videoElement.srcObject = stream;
    })
    .catch(function (error) {
        console.error('Error accessing the webcam:', error);
    });
    
    const flipSwitch = document.getElementById('flip-switch');
    const animatedDiv = document.getElementById('chat-container');
    
    flipSwitch.addEventListener('change', function() {
      if (this.checked) {
        animatedDiv.classList.add('shrink');
        animatedDiv.classList.remove('grow');
      } else {
        animatedDiv.classList.add('grow');
        animatedDiv.classList.remove('shrink');
      }
    });

    
    
}); 


// api connect
// certificates
// configuration of api's
// ping test