class Weight {
	constructor(a,b) {
		this.a = a;
		this.b = b;
 }
	weight() {
		if(this.a === '' && this.b === '') {
			return 'equal';
		}
		let alpha = 'abcdefghijklmnopqrstuvwxyz';
		let count = 0;
		let count1 = 0;
		for(let i=0;i<alpha.length;i++) {
			if(this.a[i]) {
				count+=alpha.indexOf(this.a[i]);
			}
			if(this.b[i]) {
				count1+=alpha.indexOf(this.b[i]);
			}
		}
		if(count>count1){
			return 1;
		} else if(count1>count) {
			return 2;
		} else {
			return 'equal';
		}
	}
}
function strWeight(a,b){
 let w1 = new Weight(a,b);
 return w1.weight();
}