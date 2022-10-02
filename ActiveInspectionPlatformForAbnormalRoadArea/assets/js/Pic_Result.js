class Pic_Result {
    constructor(texture, outline) {
        this.texture = texture;
        this.outline = outline;
    }
    Set_Position(x, y, z) {
        this.texture.position.set(x, y, z);
        this.outline.position.set(x, y, z);
    }
    Set_Rotation(y){
        this.texture.rotation.y = y;
        this.outline.rotation.y = y;
    }
}