{
  description = "A very basic flake";

  inputs = { nixpkgs.url = "github:/nixos/nixpkgs/nixos-22.11"; };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        musthe = pypkgs:
          pypkgs.buildPythonPackage rec {
            pname = "musthe";
            version = "1.0.0";
            src = pypkgs.fetchPypi {
              inherit pname version;
              sha256 = "RoJaf8v2OOJhcnfC3fzqxljgn6uXRuK/8XyaVIJ49u4=";
            };
          };
        py = pkgs.python39.withPackages (p: [ p.ipython (musthe p) ]);
      in {
        devShells.default =
          pkgs.mkShell { buildInputs = [ pkgs.lilypond-with-fonts py ]; };
      });

}
