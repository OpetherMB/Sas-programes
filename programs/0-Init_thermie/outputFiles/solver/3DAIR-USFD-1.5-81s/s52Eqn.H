fvScalarMatrix s52Eqn
(
fvm::ddt(s52)
+ fvm::div(phi, s52)
- fvm::laplacian(Ds+turbulence->nut()/Sct, s52)
==
fvOptions(s52)
);

s52Eqn.relax();
fvOptions.constrain(s52Eqn);
s52Eqn.solve();
fvOptions.correct(s52);
