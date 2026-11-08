function holdButton(id, key) {
    const b = document.getElementById(id);

    b.addEventListener("pointerdown", e => {
        e.preventDefault();

        b.setPointerCapture(e.pointerId);
        keys[key] = true;

        if (key === "jump" &&
            player.grounded &&
            state === "playing") {

            player.vy = -13;
            player.grounded = false;
        }

        if (key === "attack") {
            playerAttack();
        }
    });

    function release(e) {
        keys[key] = false;
    }

    b.addEventListener("pointerup", release);
    b.addEventListener("pointercancel", release);
    b.addEventListener("lostpointercapture", release);
}
