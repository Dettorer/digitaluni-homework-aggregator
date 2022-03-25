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

    # Define a devShell that contains all the Python packages listed in
    # requirements.txt
    pythonShell = mach-nix.mkPythonShell {
      requirements = builtins.readFile ./requirements.txt;
    };
  in
  {
    devShells.${system}.default = pythonShell;
  };
}
