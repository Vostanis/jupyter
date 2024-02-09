{
  inputs = {
    nixpkgs = {
      url = "github:nixos/nixpkgs/nixos-unstable";
    };
    flake-utils = {
      url = "github:numtide/flake-utils";
    };
  };
  outputs = { nixpkgs, flake-utils, ... }: flake-utils.lib.eachDefaultSystem (system:
    let
      pkgs = import nixpkgs {
        inherit system;
      };
    in rec {
      devShell = pkgs.mkShell {
        buildInputs = with pkgs; [
          (python3.withPackages(ps: with ps; [
            # core packages
            ipython
            jupyter
            numpy
            pandas
            matplotlib
            seaborn
            requests
            zipfile2
            yfinance
            mplfinance
            dash
          ]))
        ];
        shellHook = "jupyter notebook & disown";
      };
    }
  );
}
