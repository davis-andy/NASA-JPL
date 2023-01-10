function move(){
    let bar = $('.progress-bar');
    let complete = 0;
    let overlay = $('.loading-overlay');

    let id = setInterval(frame, 25);

    function frame(){
        if (complete >= 320) {
            clearInterval(id);
            overlay.css('display', 'none');
        } else {
            complete += 10;
            bar.css('width', complete + '%');
        }
    }
}

move();
