(function (window) {

	var msgPanel 	= document.getElementById('msgPanelBody');
	var inputFld 	= document.getElementById('inputFld');
	var sendButton 	= document.getElementById('sendButton');

	var sio;

	/**
	 * Strings with message templates
	 */
	var MessageTemplate = {
		// Alert template
		alert : '<div class="row alert"> \
			        <div class="msg alert"> \
			            <p><i class="fa fa-lightbulb-o"></i> {msg}</p> \
			        </div>\
			    </div>',

		they : '<div class="row they">\
					<div class="msg they">\
						<p><strong>Stranger:</strong></p>\
						<div>{msg}</div>\
					</div>\
				</div>',


		me : '<div class="row me">\
		    <div class="msg me">\
		        <p><strong>Me:</strong></p>\
		        <div>{msg}</div>\
		    </div>\
		</div>',
	};

	/**
	 * Constant values for Keys
	 */
	var Keys = {
		SHIFT : 16,
		ENTER : 13,
		RETURN : 10,
	};

	/**
	 * Chat namespace for main chat functions
	 * @type {Object}
	 */
	var Chat = {
		// Flags namespace
		flags : {
			holding : {
				shift : false,
			},
		},

		// Render namespace
		render : {
			// Renders a message based on a template
			message : function (template, msg) {
				if(template && msg){
					if(msg.indexOf('\n') != -1){
						msg = msg.split('\n');
						msg = '<p>' + msg.join('</p><p>') + '</p>';
					}else{
						console.log('Tem \n');
						msg = '<p>' + msg + '</p>';
					}

					// Replaces {msg} token for desired message
					var s = template.replace('{msg}', msg);
					var msgDOM = $(s);
					$(msgPanel).append(msgDOM);
				}
			},

			// Message namespace
			msg : {
				me : function (msg) {
					Chat.render.message(MessageTemplate.me,msg);
				},

				they : function (msg) {
					Chat.render.message(MessageTemplate.they,msg);
				},

				alert : function (msg) {
					Chat.render.message(MessageTemplate.alert,msg);
				}
			},
		},

		// Scroll namespace
		scroll : {
			top : function () {
				msgPanel.scrollTop = 0;
			},

			bottom : function () {
				msgPanel.scrollTop = msgPanel.scrollHeight;
			},
		},

		socket : {
			_namespace : '/chat',

			connect : function () {
				console.log('Initializing socket.');
				sio = io.connect('http://' + document.domain + ':' + location.port + this._namespace);
				console.log('Socket up: ', sio);
			},

			/**
			 * Send the text message through scoket.
			 */
			send : function (msg) {
				sio.send(msg);
			},

			/**
			 * Receives a text message from socket.
			 */
			receive : function (msg) {
				Chat.render.msg.they(msg);
				Chat.scroll.bottom();
			},

			alert : function (msg) {
				console.log('alert: ', msg);
				Chat.render.msg.alert(msg);
			},
		},

		/**
		 * Callback fired when key is released
		 * while input field is focussed.
		 */
		onKeyUp : function (e) {
			if(e.which == Keys.SHIFT){
				Chat.flags.holding.shift = false;
			}

			if(e.which == Keys.ENTER || e.which == Keys.RETURN){
				if(Chat.flags.holding.shift){
					// do nothing because line breaking is textarea default behaviour
				}else{
					e.preventDefault();
					Chat.sendMessage();
					return;
				}
			}
		},

		/**
		 * Callback fired when key is pressed
		 * while input field is focussed.
		 */
		onKeyDown : function (e) {
			if(e.which == Keys.SHIFT){
				Chat.flags.holding.shift = true;
			}
		},

		/**
		 * Sends the message through the socket
		 * and renders it to the panel.
		 */
		sendMessage : function () {
			var msgString = inputFld.value;
			inputFld.value = '';
			Chat.render.msg.me(msgString);
			Chat.socket.send(msgString);
			Chat.scroll.bottom();
		},

		/**
		 * Callback fired when send button clicked.
		 */
		sendButtonClicked : function () {
			Chat.sendMessage();
		},

		/**
		 * Initializes Chat
		 */
		initialize : function () {
			console.log('Initializing.');
			inputFld.addEventListener('keydown', Chat.onKeyDown);
			inputFld.addEventListener('keyup', Chat.onKeyUp);
			sendButton.addEventListener('click', Chat.sendButtonClicked);

			Chat.socket.connect();
			sio.on('message', Chat.socket.receive);
			sio.on('alert', function (data) {
				Chat.socket.alert(data.msg);
				Chat.scroll.bottom();
			});
		},
	};

	Chat.initialize();

	/**
	 * Exposing Chat namespace for testing
	 * @todo Remember to remove for production
	 */
	window.expose = {
		Chat : Chat,
		sio : sio,
	}

})(window);