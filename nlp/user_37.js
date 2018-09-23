class StringWeight {

    constructor(x, y) {
        this.x = x;
        this.y = y;
    }

    stringWeight() {
        
        if (this.x === '' && this.y === '') {
            return 'equal';
        }

        let words = 'abcdefghijklmnopqrstuvwxyz';
        let x_count = 0;
        let y_count = 0;

        for (let i = 0; i < words.length; i++) {
            if (this.x[i]) {
                x_count += words.indexOf(this.x[i]);
            }
            if (this.y[i]) {
                y_count += words.indexOf(this.y[i]);
            }
        }

        if (x_count > y_count) {
            return 1;
        } 
        
        else if (y_count > x_count) {
            return 2;
        } 
        
        else {
            return 'equal';
        }
    }
}

function strWeight(x, y) {
    let w1 = new StringWeight(x, y);
    return w1.stringWeight();
}