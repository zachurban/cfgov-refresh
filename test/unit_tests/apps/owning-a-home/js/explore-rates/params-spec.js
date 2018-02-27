const BASE_JS_PATH = '../../../../../../cfgov/unprocessed/apps/owning-a-home/';
const chai = require( 'chai' );
const expect = chai.expect;

const params = require( BASE_JS_PATH + 'js/explore-rates/params' );

describe( 'explore-rates:params', () => {
  it( 'should have correct default values', () => {
    expect( params['credit-score'] ).to.equal( 700 );
    expect( params['down-payment'] ).to.equal( '20,000' );
    expect( params['house-price'] ).to.equal( '200,000' );
    expect( params['loan-amount'] ).to.be.undefined;
    expect( params['location'] ).to.equal( 'AL' );
    expect( params['rate-structure'] ).to.equal( 'fixed' );
    expect( params['loan-term'] ).to.equal( 30 );
    expect( params['loan-type'] ).to.equal( 'conf' );
    expect( params['arm-type'] ).to.equal( '5-1' );
    expect( params['edited'] ).to.be.false;
    expect( params['isJumbo'] ).to.be.false;
    expect( params['isJumbo'] ).to.be.false;
    expect( params['prevLoanType'] ).to.equal( '' );
    expect( params['prevLocation'] ).to.equal( '' );
    expect( params['verbotenKeys'] ).to.be.an('array');
    expect( params['verbotenKeys'][0] ).to.equal( 9 );
    expect( params['verbotenKeys'][1] ).to.equal( 37 );
    expect( params['verbotenKeys'][2] ).to.equal( 38 );
    expect( params['verbotenKeys'][3] ).to.equal( 39 );
    expect( params['verbotenKeys'][4] ).to.equal( 40 );
    expect( params['verbotenKeys'][5] ).to.equal( 13 );
    expect( params['verbotenKeys'][6] ).to.equal( 16 );
    expect( params['update'] ).to.be.an('function');
  } );
} );
