(function(){

  function generatePDF() {

    var agencies = hud_data.counseling_agencies;
    var zip = hud_data.zip.zipcode.replace(', usa', '');
    var intro = 'The counseling agencies on this list are approved by the U.S. Department of Housing and Urban Development (HUD), and they can offer independent advice about whether a particular set of mortgage loan terms is a good fit based on your objectives and circumstances, often at little or no cost to you. This list shows you several approved agencies in your area. You can find other approved counseling agencies at the Consumer Financial Protection Bureau’s (CFPB) website: https://consumerfinance.gov/mortgagehelp or by calling 1-855-411-CFPB (2372). You can also access a list of nationwide HUD-approved counseling intermediaries at http://portal.hud.gov/hudportal/HUD?src=/ohc_nint';
    var logo = 'data:image/png;base64,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';

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
