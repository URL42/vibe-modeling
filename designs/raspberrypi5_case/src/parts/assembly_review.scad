// ---------------------------------------------------------------------------
// assembly_review.scad - raspberrypi5_case product-assembly review scene.
//
// Review geometry ONLY. Part id 90 (review_dispatch_id in assembly.json)
// dispatches to this scene; it is NEVER exported as a printable part —
// the manifest exports base (part 1) and lid (part 2) only.
//
// Both parts are modeled directly in assembly coordinates, so the contract's
// identity transforms (assembly.json, case_joint) apply trivially: the
// product assembly is base() union lid() with no extra transforms. The
// front and isometric views in assembly.json render from this single scene
// (the view cameras are applied by the build tool).
// ---------------------------------------------------------------------------

module assembly_review(view_id = 0, show_proxies = true) {
    assert(view_id == 0 && show_proxies,
        str("assembly_review: unsupported options view_id=", view_id,
            " show_proxies=", show_proxies));
    // base() occupies z 0..107; lid() occupies z 107..125.
    union() {
        base();
        lid();
    }
}