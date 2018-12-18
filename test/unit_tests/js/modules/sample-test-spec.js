const sampleTestIndex = require(
  '../../../../cfgov/unprocessed/js/modules/sample-test.js'
);

describe( 'sample test javascript file', () => {

  it( 'should return a string', () => {
    expect( sampleTestIndex.init() ).toBe( 'blah' );
  } );

} );
