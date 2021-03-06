/*
 * Functions for working with canvas elements
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

function resize_canvas(canvas_id) {
	canvas = document.getElementById(canvas_id);
	if (canvas) {
		canvas.width = window.innerWidth;
		canvas.height = window.innerHeight;
	}
}

function set_canvas_text(canvas_id, message) {
	var canvas = document.getElementById(canvas_id);
	if (canvas) {
		var ctx = canvas.getContext("2d");
		ctx.font = "30px Arial";
		ctx.fillText(message, 50, 50);
	}
}

function set_canvas_image(canvas_id, img) {
	var canvas = document.getElementById(canvas_id);
	if (canvas) {
		var ctx = canvas.getContext("2d");
		ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
	}
}
