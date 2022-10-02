class CIoT {
    constructor() {
        this.points = [];
    }
    Add_Point(name,color, lat, lon, earthquake, rain, mudslide) {
        let color_num = 0;
        switch (color) {
            case 'red':
                color_num = 9;
                break;
            case 'orange':
                color_num = 7;
                break;
            case 'yellow':
                color_num = 5;
                break;
            case 'green':
                color_num = 3;
                break;
            default:
                color_num = 0;
        }
        this.points.push({
            name: name,
            earthquake: earthquake,
            rainfall: rain,
            mudslide: mudslide,
            color: color_num,
            point: [lat, lon, 0]
        });
    }
    Get_Points() {
        return this.points;
    }
}
