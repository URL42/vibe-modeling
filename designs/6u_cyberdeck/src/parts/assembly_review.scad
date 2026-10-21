module assembly_review(id) {
  if(id==0) colored_product();
  else if(id==2) colored_enclosure();
  else if(id==1) colored_product(22);
  else if(id>=11 && id<=14) installed_leaf(id-10);
  else if(id==50) colored_cover();
  else if(id==51) installed_cover(6);
  else if(id==52) installed_cover(7);
  else if(id==53) cover_coupon();
  else if(id==54 || id==55) {
    v=(id==54 ? -1 : 1)*cover_station_v;
    intersection() {
      colored_cover();
      translate([-5,-4,cover_center_z+v-0.3]) cube([25,12,0.6]);
    }
  }
  else if(id==15) installed_bridge();
  else if(id==40) {
    // Interior rear-center crop includes every real printable owner.
    intersection() { colored_product(); translate([-26,65,-26]) cube([52,16,52]); }
  }
  else if(id==41) {
    intersection() { colored_product(); translate([-26,65,11.7]) cube([52,16,0.6]); }
  }
  else if(id==42) {
    intersection() { colored_enclosure(); translate([-26,65,-26]) cube([52,16,52]); }
  }
  else if(id==20) seam_station_coupon();
  else if(id>=30 && id<=37) {
    // Installed-artifact-bound normal sections, one per station.
    s=stations[id-30];
    intersection() {
      colored_product();
      station_frame(s) translate([-4,-0.3,-1]) cube([24,0.6,ring_band+2]);
    }
  }
}
