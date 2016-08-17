/*
 * Functions for working with image and sound media
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

function ManagedAudio() {
	this.audio = null;
	this.error = false;
}

function ManagedImage() {
	this.image = null;
	this.loaded = false;
	this.error = false;
}

function load_managed_audio(audio_src) {
	var wrapper = new ManagedAudio();
	wrapper.audio = new Audio();
	wrapper.audio.preload = "auto";
	wrapper.audio.onerror = function(){wrapper.error = true;};
	wrapper.audio.src = audio_src;
	return wrapper;
}

function load_managed_image(img_src) {
	var wrapper = new ManagedImage();
	wrapper.image = new Image();
	wrapper.image.onload = function(){wrapper.loaded = true;};
	wrapper.image.onerror = function(){wrapper.error = true;};
	wrapper.image.src = img_src;
	return wrapper;
}
