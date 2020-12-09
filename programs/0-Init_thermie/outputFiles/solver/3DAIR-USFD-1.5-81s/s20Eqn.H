fvScalarMatrix s20Eqn
(
fvm::ddt(s20)
+ fvm::div(phi, s20)
- fvm::laplacian(Ds+turbulence->nut()/Sct, s20)
==
fvOptions(s20)
);

s20Eqn.relax();
fvOptions.constrain(s20Eqn);
s20Eqn.solve();
fvOptions.correct(s20);
