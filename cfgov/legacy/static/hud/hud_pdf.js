(function(){

  function generatePDF() {

    var agencies = hud_data.counseling_agencies;
    var zip = hud_data.zip.zipcode.replace(', usa', '');
    var intro = 'The counseling agencies on this list are approved by the U.S. Department of Housing and Urban Development (HUD), and they can offer independent advice about whether a particular set of mortgage loan terms is a good fit based on your objectives and circumstances, often at little or no cost to you. This list shows you several approved agencies in your area. You can find other approved counseling agencies at the Consumer Financial Protection Bureau’s (CFPB) website: https://consumerfinance.gov/mortgagehelp or by calling 1-855-411-CFPB (2372). You can also access a list of nationwide HUD-approved counseling intermediaries at http://portal.hud.gov/hudportal/HUD?src=/ohc_nint';
    var logo = 'data:image/jpeg;base64,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';

    var doc = new jsPDF('p', 'in', 'letter');

    doc.setLineWidth(0.04);
    doc.setFontSize(14);
    doc.setFontStyle('bold');
    doc.text(.75, 1, 'Housing counselors near you');
    doc.addImage(logo, 'JPG', 5.7, .8, 2, .44);

    doc.setFontSize(12);
    doc.setFontStyle('normal');
    doc.text(.75, 1.4, '10 closest results to zip code ' + zip + '.');
    doc.text(.75, 1.8, doc.splitTextToSize(intro, 7));
    doc.line(.75, 3.45, 7.75, 3.45);

    // Page 1
    var offset = printAgency(agencies[0], {x: .75, y: 4});
    printAgency(agencies[1], {x: .75, y: offset + .5});

    // Page 2
    doc.addPage();
    offset = printAgency(agencies[2], {x: .75, y: .75});
    offset = printAgency(agencies[3], {x: .75, y: offset + .5});
    printAgency(agencies[4], {x: .75, y: offset + .5});

    // Page 3
    doc.addPage();
    offset = printAgency(agencies[5], {x: .75, y: .75});
    offset = printAgency(agencies[6], {x: .75, y: offset + .5});
    printAgency(agencies[7], {x: .75, y: offset + .5});

    // Page 4
    doc.addPage();
    offset = printAgency(agencies[8], {x: .75, y: .75});
    printAgency(agencies[9], {x: .75, y: offset + .5});

    function printAgency(agency, coords) {
      var x = coords.x,
          y = coords.y;
      var yOffset = 0;
      var title = doc.splitTextToSize(agency.nme, 6.5);
      var services = doc.splitTextToSize(agency.services.replace('&#44;', ','), 6);
      var info = [
        agency.adr1,
        agency.city + " " + agency.statecd + " " + agency.zipcd,
        "",
        "Website: " + agency.weburl,
        "Phone: " + agency.phone1,
        "Email: " + agency.email,
        "Languages: " + agency.languages,
        "Services: " + services.shift()
      ];
      if (agency.adr2.trim()) {
        info.splice(1, 0, agency.adr2);
      }

      doc.setFontStyle('bold');
      doc.text(x, y, title);

      yOffset += title.length;
      doc.setFontStyle('normal');
      doc.text(x, y + (.3 * yOffset), info.concat(services));

      yOffset = y + 1.75 + (.2 * (yOffset + services.length));
      if (agency.adr2.trim()) {
        yOffset += .2;
      }
      doc.setLineWidth(0.01);
      doc.line(.75, yOffset, 7.75, yOffset);
      return yOffset;
    }

    doc.save(zip + '-counselors.pdf');

  }

  $('#generate-pdf-link').on('click', function downloadPDF(ev) {
    ev.preventDefault();
    $.getScript('/static/hud/jspdf.min.js', generatePDF);
  });

})();
