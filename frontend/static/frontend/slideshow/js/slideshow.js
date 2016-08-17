/*
 * JavaScript slideshow implementation. Slides and audio files are preloaded
 * at 50% of the display interval, in order to avoid flicker at slide switch
 * time.
 *
 * Author:   Dr. Mike Murphy <mmurphy2@coastal.edu>
 * Revision: 5 February 2016
 *
 * Copyright 2016 Coastal Carolina University
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
*/

// Global slideshow tracker
var SlideShow = {
	run: true,
	slideset: null,
	index: -1,
	display_length: 0, // milliseconds!
	canvas_id: null,
	sound_id: null,
	next_img: null,
	next_sound: null,
	current_sound: null
};


function preload_slide() {
	var timeout = 0;
	if (SlideShow.slideset) {
		SlideShow.index++;
		
		if (SlideShow.index < SlideShow.slideset.slides.length) {
			if (SlideShow.index >= 0) {
				timeout = SlideShow.display_length / 2;
			}
			
			var slide_name = SlideShow.slideset.slides[SlideShow.index];
			var slide = SlideShow.slideset[slide_name];
			
			if ("image" in slide) {
				SlideShow.next_img = load_managed_image(slide.image);
			}
			else {
				SlideShow.next_img = null;
			}
			
			if ("time" in slide) {
				SlideShow.display_length = slide.time * 1000;
			}
			else {
				SlideShow.display_length = 10000;
			}
			
			if ("sound" in slide) {
				SlideShow.next_sound = load_managed_audio(slide.sound);
			}
			else {
				SlideShow.next_sound = null;
			}
		}
		else {
			timeout = SlideShow.display_length / 2;
			SlideShow.run = false;
			SlideShow.next_img = null;
			SlideShow.next_sound = null;
		}
	}
	
	setTimeout(switch_slide, timeout);
}

function switch_sound() {
	if (SlideShow.current_sound) {
		SlideShow.current_sound.audio.pause();
	}
	
	if (SlideShow.next_sound) {
		SlideShow.current_sound = SlideShow.next_sound;
		SlideShow.next_sound = null;
		if (! SlideShow.current_sound.error) {
			SlideShow.current_sound.audio.play();
		}
	}
	else {
		SlideShow.current_sound = null;
	}
}

function switch_image() {
	if (SlideShow.next_img) {
		if (! SlideShow.next_img.error) {
			set_canvas_image(SlideShow.canvas_id, SlideShow.next_img.image);
		}
	}
}

function switch_slide() {
	var image_ready = false;
	
	if (SlideShow.run) {
	
		// If a next image is specified, see if it's ready
		if (SlideShow.next_img) {
			if (SlideShow.next_img.error || SlideShow.next_img.loaded) {
				// Will skip current image on error
				image_ready = true;
			}
		}
		else {
			// Control file might specify a new sound with no new image
			image_ready = true;
		}
		
		if (image_ready) {
			switch_image();
			switch_sound();
			
			var next_time = SlideShow.display_length / 2;
			setTimeout(preload_slide, next_time);
		}
		else {
			setTimeout(switch_slide, 150);
		}
	}
	else {
		// Reload the page at the end of the slideshow
		location.reload(true);
	}
}

function start_slideshow() {
	set_canvas_text(SlideShow.canvas_id, "Please wait...");
	preload_slide();
}
