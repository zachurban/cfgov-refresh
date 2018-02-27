const BASE_JS_PATH = '../../../../../../cfgov/unprocessed/apps/owning-a-home/';
const chai = require( 'chai' );
const expect = chai.expect;

const params = require( BASE_JS_PATH + 'js/explore-rates/params' );

describe( 'explore-rates:params', () => {
  it( 'should have correct default values', () => {

    expect( params['credit-score'] ).to.equal( 700 );
  } );
} );
