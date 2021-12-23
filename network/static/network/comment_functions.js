// Handles POST request and single comment appearance after like
function likeCommentControl(commentNode) {
  let element = commentNode.querySelector(".like-panel")
  //Handle like comment
  element.addEventListener('click', (event) => {
    let csrftoken = getCookie('csrftoken');
    let emojiType;

    // Look for event's emoji type
    // Check if like button is a target
    if (event.target.name === "like") {
      emojiType = event.target.name;
    }
    //Check if emoji list is a target
    else if (typeof event.target.dataset.name === "string") {
      emojiType = event.target.dataset.name;
    }
    else {
      return false;
    }
    // Already liked - update like'e emoji type
    if (commentNode.querySelector(".like-button").classList.contains("liked")) {
      fetch(`/like/comment/${commentNode.id.substr(8)}`, {
        method: "PUT",
        body: JSON.stringify({
          emojiType: emojiType
        }),
        headers: { "X-CSRFToken": csrftoken }
      })
        .then(async (response) => {
          // Successful like -> update comment view
          if (response.status === 201) {
            console.log(`comment id: ${commentNode.id.substr(8)} like updated successfully`)
            // Update like button emoji and class
            updateCommentLikeIcon(commentNode);
            // Update like counter and emoji list
            let previousEmojiType = commentNode.querySelector(".like-button > i").dataset.name;
            updateEmojiList(commentNode, emojiType, previousEmojiType);
            // Reconnect like amount indicator event to each emoji
            likesAmountIndicatorControl(commentNode);
          }
          else {
            let response_body = await response.json();

            throw new Error(response_body.error);
          }
        })
        .catch(error => {
          alert(error);
          location.reload();
        })
    }
    // Not liked yet - save like
    else {
      fetch(`/like/comment/${commentNode.id.substr(8)}`, {
        method: "POST",

      })
    }
  })
}
