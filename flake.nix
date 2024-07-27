{
  description = "Basic flake for multisystem nixpkgs";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-23.11";

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem
    (system: let 
      pkgs = nixpkgs.legacyPackages.${system}; 
      lib = pkgs.lib;
      lilypond = pkgs.lilypond-with-fonts.overrideAttrs(rec {
        version = "2.23.6";
        src = pkgs.fetchurl {
          url = "http://lilypond.org/download/sources/v${lib.versions.majorMinor version}/lilypond-${version}.tar.gz";
          sha256 = "sha256-oXm9l0oOZDkO/vW7DMHnKH8SGCN1SEM626UcTyW7os4=";
        };
      });
      mkAbjad = ps: ps.abjad.override {inherit lilypond;};
      py = pkgs.python3.withPackages (ps: with ps; [genanki ipython (mkAbjad ps)]);
    in {
      devShells.default = pkgs.mkShell {
        buildInputs = [ py ];
        # buildInputs = [ py lilypond];
      };
    });
}
