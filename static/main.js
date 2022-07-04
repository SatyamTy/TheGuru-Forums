//Navbar
function hideIconBar(){
    var iconBar = document.getElementById("iconBar");
    var navigation = document.getElementById("navigation");
    iconBar.setAttribute("style", "display:none;");
    navigation.classList.remove("hide");
}

function showIconbar(){
    var iconBar = document.getElementById("iconBar");
    var navigation = document.getElementById("navigation");
    iconBar.setAttribute("style", "display:block;");
    navigation.classList.add("hide");
}

//comment

function showComment(){
    var commentArea = document.getElementById("comment-area");
    commentArea.setAttribute("style", "display:block;");
}

//reply

function showReply(id){
    var replyArea = document.getElementById(id);
    replyArea.setAttribute("style", "display:block;");
}

//replies
function showReplies(id){
    var repliesArea = document.getElementById(id);
    repliesArea.setAttribute("style", "display:block;");
}