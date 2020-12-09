fvScalarMatrix s70Eqn
(
fvm::ddt(s70)
+ fvm::div(phi, s70)
- fvm::laplacian(Ds+turbulence->nut()/Sct, s70)
==
fvOptions(s70)
);

s70Eqn.relax();
fvOptions.constrain(s70Eqn);
s70Eqn.solve();
fvOptions.correct(s70);
