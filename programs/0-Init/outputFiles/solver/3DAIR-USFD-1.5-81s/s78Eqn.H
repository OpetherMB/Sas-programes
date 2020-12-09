fvScalarMatrix s78Eqn
(
fvm::ddt(s78)
+ fvm::div(phi, s78)
- fvm::laplacian(Ds+turbulence->nut()/Sct, s78)
==
fvOptions(s78)
);

s78Eqn.relax();
fvOptions.constrain(s78Eqn);
s78Eqn.solve();
fvOptions.correct(s78);
