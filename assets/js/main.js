(function (window) {

	var msgPanel 	= document.getElementById('msgPanelBody');
	var inputFld 	= document.getElementById('inputFld');
	var sendButton 	= document.getElementById('sendButton');
	var skipButton 	= document.getElementById('skipButton');

	var sio;

	/**
	 * Strings with message templates
	 */
	var MessageTemplate = {
		icon : {
			ALERT : '<i class="fa fa-lightbulb-o"></i>',
			LOAD  : '<i class="fa fa-circle-o-notch fa-spin"></i>',
		},

		// Alert template
		alert : '<div class="row alert"> \
			        <div class="msg alert"> \
			            <p><i class="fa fa-lightbulb-o"></i> {msg}</p> \
			        </div>\
			    </div>',

	    customAlert : 	'<div class="row alert"> \
					        <div class="msg alert"> \
					            <p>{ico} {msg}</p> \
					        </div>\
					    </div>',

		they : '<div class="row they">\
					<div class="msg they">\
						<p><strong>Stranger:</strong></p>\
						<div>{msg}</div>\
					</div>\
				</div>',


		me : 	'<div class="row me">\
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
		F5 : 116,
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
			skip : false,
			alone : true,
		},

		// Render namespace for message rendering related methods
		render : {
			// Renders a message based on a template
			message : function (template, msg, ico) {
				if(template && msg) {
					if(template != MessageTemplate.alert && template != MessageTemplate.customAlert){
						if(msg.indexOf('\n') != -1){
							msg = msg.split('\n');
							msg = '<p>' + msg.join('</p><p>') + '</p>';
						}else{
							console.log('Tem \n');
							msg = '<p>' + msg + '</p>';
						}
					}

					// Replaces {msg} token for desired message
					var s = template.replace('{msg}', msg);
					if(template == MessageTemplate.customAlert && ico){
						s = s.replace('{ico}', ico);
					}
					var msgDOM = $(s);
					$(msgPanel).append(msgDOM);
				}
			},

			/**
			 * Clear message panel messages
			 */
			clear : function () {
				msgPanel.innerHTML = '';
			},

			// Message shortcut namespace for easing access to message rendering methods
			msg : {
				me : function (msg) {
					Chat.render.message(MessageTemplate.me,msg);
				},

				they : function (msg) {
					Chat.render.message(MessageTemplate.they,msg);
				},

				alert : function (msg, ico) {
					ico = ico == undefined ? MessageTemplate.icon.ALERT : ico;
					Chat.render.message(MessageTemplate.customAlert,msg,ico);
				}
			},
			
		},

		// Scroll namespace for message panel scrolling related methods
		scroll : {
			top : function () {
				msgPanel.scrollTop = 0;
			},

			bottom : function () {
				msgPanel.scrollTop = msgPanel.scrollHeight;
			},
		},

		// Socket namespace for icoming socket packet handling related methods
		socket : {
			_namespace : '/chat',

			/**
			 * EVENT TABLE
			 * Default built-in SocketIO events are not in the table
			 */
			events : {
				PAIRFOUND 	: 'pairfound',
				PAIRLOST 	: 'pairlost',
				ALERT 		: 'alert',
				SKIP  		: 'skip',
			},

			connect : function () {
				console.log('Initializing socket.');
				var protocol = window.location.href.substr(0,window.location.href.indexOf(':'));
				protocol += '://';
				var where = protocol + document.domain + ':' + location.port + this._namespace;
				console.log('Where: ', where);
				sio = io.connect(where);
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

			/**
			 * Receives an alert from socket
			 */
			alert : function (msg, ico) {
				console.log('alert: ', msg);
				Chat.render.msg.alert(msg);
			},

			skip : function () {
				console.log('Called skip.');
				sio.emit(Chat.socket.events.SKIP);
			},

			/**
			 * Receives an onPairFound event from socket.
			 * That means someone is connected 
			 * and ready to start chatting.
			 */
			onPairFound : function (data) {
				console.log('onPairFound');
				Chat.flags.alone = false;
				Chat.render.clear();
				Chat.render.msg.alert(data.msg);
				Chat.scroll.bottom();
				// Enable inputs once pair is connected.
				Chat.input.enable();
			},

			/**
			 * Receives an onPairLost event from socket.
			 * That means stranger has disconnected and
			 * current user must search for another pair.
			 */
			onPairLost : function (data) {
				console.log('pairlost');
				Chat.flags.alone = true;
				Chat.render.msg.alert(data.msg);
				Chat.scroll.bottom();
				// Disable inputs after pair disconnected.
				Chat.input.disable();
			},

		},

		// Input namespace for input management related methods
		input : {
			/**
			 * Disables all chat input.
			 */
			disable : function () {
				inputFld.disabled = 'disabled';
				$(inputFld).addClass('disabled');

				sendButton.disabled = true;
				$(sendButton).addClass('disabled');
			},

			/**
			 * Enables all chat input.
			 */
			enable : function () {
				inputFld.disabled = false;
				$(inputFld).removeClass('disabled');

				sendButton.disabled = false;
				$(sendButton).removeClass('disabled');
			},

			/**
			 * Namespace for skip button.
			 */
			skip : {
				// Enables skip button.
				enable : function () {
					var btn = $(skipButton);
					if(btn.hasClass('disabled')){
						btn.removeClass('disabled');
					}
				},

				// Disbles skip button.
				disable : function () {
					var btn = $(skipButton);
					if(!btn.hasClass('disabled')){
						btn.addClass('disabled');
					}
				},
			}
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

		skipConversation : function () {
			var btn = $(skipButton);

			if(btn.hasClass('confirm')){
				btn.removeClass('confirm');
				btn.addClass('skip');
			}

			Chat.flags.skip = false;
			Chat.flags.alone = false;
			Chat.socket.skip();
			Chat.render.clear();
			Chat.render.msg.alert('Connecting to someone...', MessageTemplate.icon.LOAD);
			Chat.scroll.bottom();
			Chat.input.disable();
		},

		/**
		 * Callback fired when send button clicked.
		 */
		sendButtonClicked : function () {
			Chat.sendMessage();
		},

		/**
		 * Callback fired when skip button is clicked.
		 * Also fired when ESC is pressed. 
		 * If pressed twice skips the conversation.
		 */
		skipButtonCliked : function () {
			var btn = $(skipButton);

			if(Chat.flags.alone){ // User is alone
				Chat.skipConversation();

			}else{
				if(btn.hasClass('confirm')){ // If user had called skip already, confirm the conversation skipping
					Chat.flags.skip = false;
					Chat.skipConversation();
				}else{ // I user hadn't called skip yet, ask for confirmation
					Chat.flags.skip = true;

					if(btn.hasClass('skip')){
						btn.removeClass('skip');
					}

					btn.addClass('confirm');
				}

			}
		},

		/**
		 * Initializes Chat
		 */
		initialize : function () {
			console.log('Initializing.');
			inputFld.addEventListener('keydown', Chat.onKeyDown);
			inputFld.addEventListener('keyup', Chat.onKeyUp);
			sendButton.addEventListener('click', Chat.sendButtonClicked);
			skipButton.addEventListener('click', Chat.skipButtonCliked);

			// This event handler prevents the page to be
			// unloaded or refreshed unintentionally by the user
			window.addEventListener('beforeunload', function (e) {
				// Although we have a custom message 
				// here it will most likely not be 
				// displayed to the user by the browser
				var dialogText = 'Are you sure you want to leave? :/';
				e.preventDefault();
				e.returnValue = dialogText;
				return dialogText;
			});

			Chat.socket.connect();
			sio.on('message', Chat.socket.receive);

			sio.on(Chat.socket.events.PAIRFOUND, function (data) {
				Chat.socket.onPairFound(data);
			});

			sio.on(Chat.socket.events.PAIRLOST, function (data) {
				Chat.socket.onPairLost(data);
			});

			sio.on(Chat.socket.events.ALERT, function (data) {
				console.log('alert');
				if(data.type){
					Chat.socket.alert(data.msg, data.type);
				}else{
					Chat.socket.alert(data.msg);
				}
				Chat.scroll.bottom();
			});

			// Disable inputs until pair is connected.
			Chat.input.disable();

			Chat.render.msg.alert('Connecting to someone...', MessageTemplate.icon.LOAD);
		},
	};

	Chat.initialize();

	/**
	 * Exposing Chat namespace for testing
	 * @todo Remember to remove for production
	 */
	window.expose = {
		Chat : Chat,
		MessageTemplate : MessageTemplate,
		sio : sio,
	}

})(window);