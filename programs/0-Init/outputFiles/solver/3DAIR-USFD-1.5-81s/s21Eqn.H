fvScalarMatrix s21Eqn
(
fvm::ddt(s21)
+ fvm::div(phi, s21)
- fvm::laplacian(Ds+turbulence->nut()/Sct, s21)
==
fvOptions(s21)
);

s21Eqn.relax();
fvOptions.constrain(s21Eqn);
s21Eqn.solve();
fvOptions.correct(s21);
