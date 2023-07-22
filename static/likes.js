BASE_URL = "http://localhost:5000/";

$(document).on("click", "#messages-form", async function (evt) {
	evt.preventDefault();
	msg_id = $(this).attr("data-msg-id");

	// Add to liked
	if ($(this).hasClass("btn-secondary")) {
		await axios.post(`${BASE_URL}messages/add_like`, {
			message_id: msg_id,
		});
		$(this).toggleClass("btn-secondary");
		$(this).toggleClass("btn-primary");
	}

	// Remove from liked
	else if ($(this).hasClass("btn-primary")) {
		await axios.post(`${BASE_URL}messages/remove_like`, {
			message_id: msg_id,
		});
		$(this).toggleClass("btn-primary");
		$(this).toggleClass("btn-secondary");
	}
});
