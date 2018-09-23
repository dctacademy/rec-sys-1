class Weight {
	constructor(a,b) {
		this.str = a;
		this.str1 = b
	}
	compare() {
		let sum = 0;
		let sum1 =0;
		const alp = 'abcdefghijklmnopqrstuvwxyz';
		for(var i=0;i<alp.length;i++) {
			for(var j =0;j<this.str.length;j++) {
				if(this.str[j] === alp[i]) {
					sum += i+1;
				}
			};
		 for(var k=0; k<this.str1.length;k++) {
			if(this.str1[k] == alp[i]){
				sum1 += i+1;
			}
		};
			if(sum > sum1){
				return 2;
			} else if(sum < sum1) {
				return 1;
			} else {
				return 'equal';
			}
		}
	}
}

function strWeight(a,b){
	let w1 = new Weight(a,b);
	return w1.compare();
}class Weight {
	constructor(a,b) {
		this.str = a;
		this.str1 = b
	}
	compare() {
		let sum = 0;
		let sum1 =0;
		const alp = 'abcdefghijklmnopqrstuvwxyz';
		for(var i=0;i<alp.length;i++) {
			for(var j =0;j<this.str.length;j++) {
				if(this.str[j] === alp[i]) {
					sum += i+1;
				}
			};
		 for(var k=0; k<this.str1.length;k++) {
			if(this.str1[k] == alp[i]){
				sum1 += i+1;
			}
		};
			if(sum > sum1){
				return 2;
			} else if(sum < sum1) {
				return 1;
			} else {
				return 'equal';
			}
		}
	}
}

function strWeight(a,b){
	let w1 = new Weight(a,b);
	return w1.compare();
}class Weight {
	constructor(a,b) {
		this.str = a;
		this.str1 = b
	}
	compare() {
		let sum = 0;
		let sum1 =0;
		const alp = 'abcdefghijklmnopqrstuvwxyz';
		for(var i=0;i<alp.length;i++) {
			for(var j =0;j<this.str.length;j++) {
				if(this.str[j] === alp[i]) {
					sum += i+1;
				}
			};
		 for(var k=0; k<this.str1.length;k++) {
			if(this.str1[k] == alp[i]){
				sum1 += i+1;
			}
		};
			if(sum > sum1){
				return 2;
			} else if(sum < sum1) {
				return 1;
			} else {
				return 'equal';
			}
		}
	}
}

function strWeight(a,b){
	let w1 = new Weight(a,b);
	return w1.compare();
}