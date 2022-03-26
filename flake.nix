{
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
    utils.url = "github:numtide/flake-utils";
    mach-nix-src = {
      url = "github:DavHau/mach-nix/";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = { self, nixpkgs, utils, mach-nix-src }:
  let
    # Configure mach-nix
    system = "x86_64-linux";
    pkgs = import nixpkgs { inherit system; };
    mach-nix = import mach-nix-src { inherit pkgs; };

    version = "1.1";
    requirements = builtins.readFile ./requirements.txt;
  in
  {
    packages.${system}.default = mach-nix.buildPythonPackage rec {
      pname = "digitaluni-homework-aggregator";
      src = ./.;

      phases = [ "unpackPhase" "installPhase" ];
      installPhase = ''
        mkdir -p $out/bin
        cp -r digitaluni.py templates $out/bin/
        cp aggregator.py $out/bin/${pname}
      '';

      inherit requirements version;
    };

    devShells.${system}.default = mach-nix.mkPythonShell {
      inherit requirements;
    };
  };
}
