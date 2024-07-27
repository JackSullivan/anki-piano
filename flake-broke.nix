{
  description = "Lilypond test";

  inputs = { nixpkgs.url = "github:/nixos/nixpkgs/nixos-22.11"; };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        testfile = pkgs.writeText "file.ly" ''
          \version "2.24.0"
          { c' }
        '';
        run-lily = lp: pkgs.runCommand "run-lily" {} ''
          ${lp}/bin/lilypond ${testfile}
        '';
      in {
        packages = {
          default = run-lily pkgs.lilypond;
          with-fonts = run-lily pkgs.lilypond-with-fonts;
        };
      });
}
