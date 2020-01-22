/* global Vue audiodir */

Vue.component('annotationsaudioplayer', {
	delimiters: ['${', '}'],
	template: '#annotationsaudioplayer-template',
	props: ['audiofile'],
	data: function () {
		return {
			audio: undefined,
			audioInterval: undefined,
			loaded: false,
			duration: 0,
			aPos: 0,
			lPos: -1,
			aPosRel: 0,
			aPosProz: 0,
			paused: true,
			playing: false
		};
	},
	computed: {
		audiofileC: function () {
			var taf = this.audiofile;
			taf = taf.replace(/\\/g, '/');
			if (taf.charAt(0) === '/') {
				taf = taf.substr(1);
			}
			return taf;
		},
		audiodirC: function () {
			var tad = audiodir;
			tad = tad.replace(/\\/g, '/');
			if (!tad.slice(-1) === '/') {
				tad = tad + '/';
			}
			return tad;
		}
	},
	methods: {
		/* Steuerung */
		play: function () {
			if ((this.playing && !this.paused) || !this.loaded) return;
			this.paused = false;
			this.playing = true;
			this.audio.play();
		},
		pause: function () {
			if ((!this.playing && this.paused) || !this.loaded) return;
			this.paused = true;
			this.playing = false;
			this.audio.pause();
		},
		setAudioPos: function (e) {
			var pos = e.target.getBoundingClientRect();
			var seekPos = (e.clientX - pos.left) / pos.width;
			this.audio.currentTime = this.duration * seekPos;
		},
		setAudioPosBySec: function (sec) {
			this.audio.currentTime = sec;
		},
		fastForward: function () {
			if (!this.loaded) return;
			this.audio.currentTime = this.duration;
		},
		fastBackward: function () {
			if (!this.loaded) return;
			this.audio.currentTime = 0;
		},
		forward: function () {
			if (!this.loaded) return;
			this.audio.currentTime = this.audio.currentTime + 10;
		},
		backward: function () {
			if (!this.loaded) return;
			this.audio.currentTime = this.audio.currentTime - 10;
		},
		/* Tastatur */
		keyUp: function (e) {
			// console.log(e.keyCode);
			if (e.ctrlKey && e.keyCode === 32) { // ctrl+space
				this.$emit('ctrlkey');
				if (this.paused) {
					this.play();
				} else {
					this.pause();
				}
			} else if (e.ctrlKey && e.keyCode === 89) { // ctrl+y
				this.$emit('ctrlkey');
				this.fastBackward();
			} else if (e.ctrlKey && e.keyCode === 88) { // ctrl+x
				this.$emit('ctrlkey');
				this.fastForward();
			} else if (e.ctrlKey && e.keyCode === 50) { // ctrl+2
				this.$emit('ctrlkey');
				this.backward();
			} else if (e.ctrlKey && e.keyCode === 51) { // ctrl+3
				this.$emit('ctrlkey');
				this.forward();
			} else if (e.ctrlKey && e.keyCode === 49) { // ctrl+1
				this.$emit('ctrlkey');
				// this.stepBackward();
			} else if (e.ctrlKey && e.keyCode === 52) { // ctrl+4
				this.$emit('ctrlkey');
				// this.stepForward();
			}
		},
		/* Funktionen */
		audioPlayPause: function (e) {
			if (e.type === 'pause') {
				this.paused = true;
				this.playing = false;
			}
		},
		audioPlayingUI: function (e) {
			if (this.loaded) {
				this.aPos = this.audio.currentTime;
				if (this.aPos !== this.lPos) {
					this.lPos = this.aPos;
					this.$emit('audiopos', this.aPos);
					this.aPosRel = (this.aPos / this.duration);
					this.aPosProz = this.aPosRel * 100;
				}
			}
		},
		audioLoaded: function () {
			if (this.audio.readyState >= 2) {
				this.loaded = true;
				this.duration = this.audio.duration;
				this.$emit('audioduration', this.duration);
			} else {
				this.playing = false;
				this.paused = true;
				this.loaded = false;
				throw new Error('Audiodatei konnte nicht geladen werden!');
			}
		},
		/* Zeit umrechnen */
		durationToSeconds: function (hms) {
			var s = 0.0;
			if (hms && hms.indexOf(':') > -1) {
				var a = hms.split(':');
				if (a.length > 2) { s += parseFloat(a[a.length - 3]) * 60 * 60; }
				if (a.length > 1) { s += parseFloat(a[a.length - 2]) * 60; }
				if (a.length > 0) { s += parseFloat(a[a.length - 1]); }
			} else {
				s = parseFloat(hms);
				if (isNaN(s)) { s = 0.0; }
			}
			return s;
		},
		secondsToDuration: function (sec, fix = 6) {
			var v = '';
			if (sec < 0) { sec = -sec; v = '-'; }
			var h = parseInt(sec / 3600);
			sec %= 3600;
			var m = parseInt(sec / 60);
			var s = sec % 60;
			return v + ('0' + h).slice(-2) + ':' + ('0' + m).slice(-2) + ':' + ('0' + s.toFixed(fix)).slice(-(3 + fix));
		}
	},
	mounted: function () {
		this.audio = this.$el.querySelectorAll('audio')[0];
		this.audio.addEventListener('loadeddata', this.audioLoaded);
		this.audio.addEventListener('pause', this.audioPlayPause);
		this.audio.addEventListener('play', this.audioPlayPause);
		// this.audio.addEventListener('timeupdate', this.audioPlayingUI);
		this.audioInterval = setInterval(this.audioPlayingUI, 100);
		window.addEventListener('keyup', this.keyUp);
	},
	beforeDestroy: function () {
		this.$emit('audiopos', 0);
		clearInterval(this.audioInterval);
		// this.audio.removeEventListener('timeupdate', this.audioPlayingUI);
		this.audio.removeEventListener('loadeddata', this.audioLoaded);
		this.audio.removeEventListener('pause', this.audioPlayPause);
		this.audio.removeEventListener('play', this.audioPlayPause);
		window.removeEventListener('keyup', this.keyUp);
	}
});
